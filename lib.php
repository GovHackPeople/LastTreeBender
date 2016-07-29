<?php

interface Logger {
	function msg($message);
}

class ConsoleLogger implements Logger {
	public function msg($message) {
		echo $message . "\n";
	}
}

class NullLogger implements Logger {
	public function msg($message) {}
}

class DataManager {
	
	private $log;
	private $dataDir;
	private $treeCsv;
	private $databaseFile;
	
	public function __construct(Logger $log) {
		$this->dataDir = dirname(__FILE__) . DIRECTORY_SEPARATOR . "data";
		$this->treeCsv = $this->dataDir . DIRECTORY_SEPARATOR . "trees.csv";
		$this->databaseFile = $this->dataDir . DIRECTORY_SEPARATOR . "data.db";
		$this->log = $log;
		
		$this->log->msg("Using data dir: {$this->dataDir}");
		$this->log->msg("Using tree data from: {$this->treeCsv}");
		$this->log->msg("Using database at: {$this->databaseFile}");
	}
	
	public function connectToDb() {
		$exists = file_exists($this->databaseFile);
		
		$this->log->msg("Connecting to database");
		$db = new SQLite3($this->databaseFile);
		
		$extension = strtoupper(substr(PHP_OS, 0, 3)) === 'WIN' ? 'mod_spatialite.dll' : 'mod_spatialite.so';
		$this->log->msg("Loading {$extension} extension (make sure it is in your \"sqlite3.extension_dir\")");
		$db->loadExtension($extension);
		$db->exec("BEGIN TRANSACTION");
		$db->exec("SELECT InitSpatialMetadata()");
		$db->exec("COMMIT");
		
		if (!$exists) {
			$this->createDb($db);
		}
		
		return $db;
	}
	
	private function createDb(Sqlite3 $db) {
		$this->log->msg("Creating database for first time");
		Tree::createTable($db);
	}
	
	public function importData() {
		$this->prepareRawData();
		
		$db = $this->connectToDb();
		$trees = new TreeCsv();
		$trees->parse($this->log, $this->treeCsv, $db);
	}
	
	/**
	 * Ensure that the required data sets are downloaded and present in the
	 * data directory, ready for importing into the database.
	 */
	private function prepareRawData() {
		if (!file_exists($this->dataDir)) {
			$this->log->msg("Making directory {$this->dataDir}");
			mkdir($this->dataDir);
		}
		
		$this->prepareTreeCsv();
	}
	
	private function prepareTreeCsv() {
		if (!file_exists($this->treeCsv)) {
			$this->log->msg("Downloading tree.csv file");
			$contents = file_get_contents("https://data.melbourne.vic.gov.au/api/views/fp38-wiyy/rows.csv?accessType=DOWNLOAD");
			file_put_contents($this->treeCsv, $contents);
		} else {
			$this->log->msg("Using already existing tree.csv file");
		}
	}
	
}

class CsvParser {
	private $file;
	
	public function __construct($file) {
		$this->file = $file;
	}
	
	public function parseRows(Closure $handler) {
		$csvHandle = fopen($this->file, "r");
		
		$first = true;
		while ($row = fgetcsv($csvHandle)) {
			if ($first) {
				$headers = $row;
				$first = false;
				continue;
			}
			
			$handler(array_combine($headers, $row));
		}
	}
}

class Tree {
	
	public $comId;
	public $commonName;
	public $scientificName;
	public $genus;
	public $family;
	public $yearPlanted;
	public $lat;
	public $long;
				
	public function __construct($comId, $commonName, $scientificName, $genus,
			$family, $yearPlanted, $lat, $long) {
	
		$this->comId = $comId;
		$this->commonName = $commonName;
		$this->scientificName = $scientificName;
		$this->genus = $genus;
		$this->family = $family;
		$this->yearPlanted = $yearPlanted;
		$this->lat = $lat;
		$this->long = $long;
		
	}
	
	public function save(Logger $log, SQLite3 $db) {
		$lat = (float)$this->lat;
		$long = (float)$this->long;
		$stmt = $db->prepare(<<<sql
			INSERT INTO tree (
				comId,
				commonName,
				scientificName,
				genus,
				family,
				yearPlanted,
				latLong
			) VALUES (
				:comId,
				:commonName,
				:scientificName,
				:genus,
				:family,
				:yearPlanted,
				GeomFromText('POINT({$lat} {$long})')
			)
sql
				);
		
		$stmt->bindParam('comId', $this->comId);
		$stmt->bindParam('commonName', $this->commonName);
		$stmt->bindParam('scientificName', $this->scientificName);
		$stmt->bindParam('genus', $this->genus);
		$stmt->bindParam('family', $this->family);
		$stmt->bindParam('yearPlanted', $this->yearPlanted);
		$stmt->bindParam('lat', $this->lat);
		$stmt->bindParam('long', $this->long);
		
		if ($stmt->execute() === false) {
			throw new Exception($db->lastErrorMsg());
		}
	}
	
	public static function createTable(SQLite3 $db) {
		$db->exec(<<<sql
			CREATE TABLE IF NOT EXISTS tree (
				comId TEXT NOT NULL,
				commonName TEXT,
				scientificName TEXT,
				genus TEXT,
				family TEXT,
				yearPlanted INTEGER,
				latLong POINT NOT NULL
			)
sql
		);
	}
}

class TreeCsv {
	
	
	/**
	 * Each row of the CSV gets parsed into a PHP array that looks like this:
	 * 
	 *   [CoM ID] => 1031823
	 *   [Common Name] => White Poplar
	 *   [Scientific Name] => Populus alba
	 *   [Genus] => Populus
	 *   [Family] => Salicaceae
	 *   [Diameter Breast Height] => 64
	 *   [Year Planted] => 1998
	 *   [Date Planted] => 09/02/1998
	 *   [Age Description] => Mature
	 *   [Useful Life Expectency] => 6-10 years (<50% canopy)
	 *   [Useful Life Expectency Value] => 10
	 *   [Precinct] => South Yarra & Eastern Parklands
	 *   [Located in] => Park
	 *   [UploadDate] => 29/07/2016
	 *   [CoordinateLocation] => (-37.8320351972647, 144.976732703301)
	 *   [Latitude] => -37.8320351972647
	 *   [Longitude] => 144.976732703301
	 *   [Easting] => 321948.89
	 *   [Northing] => 5810892.1
	 * 
	 * Right now, we are only storing a subset of this, but we can choose to
	 * store more if desired/required.
	 */
	public function parse(Logger $log, $csvPath, Sqlite3 $db) {
		$i = 0;
		$handler = function(array $row) use ($db, &$i, $log) {
			$tree = new Tree(
				$row['CoM ID'],
				$row['Common Name'],
				$row['Scientific Name'],
				$row['Genus'],
				$row['Family'],
				$row['Year Planted'],
				$row['Latitude'],
				$row['Longitude']
			);
			
			$tree->save($log, $db);
			
			$i ++;
			if ($i % 5000 == 0) {
				$log->msg("  Imported {$i} trees...");
			}
		};
		
		$log->msg("Parsing .csv of trees and inserting into database (this may take some time)");
		$db->query('BEGIN TRANSACTION;');
		$parser = new CsvParser($csvPath);
		$parser->parseRows($handler);
		$db->query('COMMIT;');
	}
}