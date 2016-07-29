<?php

class DataManager {
	
	private $dataDir;
	private $treeCsv;
	private $databaseFile;
	
	public function __construct() {
		$this->dataDir = dirname(__FILE__) . DIRECTORY_SEPARATOR . "data";
		$this->treeCsv = $this->dataDir . DIRECTORY_SEPARATOR . "trees.csv";
		$this->databaseFile = $this->dataDir . DIRECTORY_SEPARATOR . "data.db";
	}
	
	public function prepare() {
		$this->prepareRawData();
		$this->prepareDatabase();
	}
	
	private function prepareDatabase() {
		$db = new PDO("sqlite:{$this->databaseFile}");
		Tree::createTable($db);
		
		$trees = new TreeCsv();
		$trees->parse($this->treeCsv, $db);
	}
	
	private function prepareRawData() {
		if (!file_exists($this->dataDir)) {
			echo "Making directory {$this->dataDir}\n";
			mkdir($this->dataDir);
		}
		
		$this->prepareTreeCsv();
	}
	
	public function prepareTreeCsv() {
		if (!file_exists($this->treeCsv)) {
			// TODO: This is not the path to the downloaded CSV, but rather the web page where we can access the CSV from.
			// I get around this by manually downloading the file and putting it in the data/ directory.
			$contents = file_get_contents("https://data.melbourne.vic.gov.au/api/views/fp38-wiyy/rows.csv?accessType=DOWNLOAD");
			file_put_contents($this->treeCsv, $contents);
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
	
	public function save(PDO $db) {
		$stmt = $db->prepare(<<<sql
			INSERT INTO tree (
				comId,
				commonName,
				scientificName,
				genus,
				family,
				yearPlanted,
				lat,
				long
			) VALUES (
				:comId,
				:commonName,
				:scientificName,
				:genus,
				:family,
				:yearPlanted,
				:lat,
				:long
			)
sql
				);
		
		$stmt->execute(array(
			'comId' => $this->comId,
			'commonName' => $this->commonName,
			'scientificName' => $this->scientificName,
			'genus' => $this->genus,
			'family' => $this->family,
			'yearPlanted' => $this->yearPlanted,
			'lat' => $this->lat,
			'long' => $this->long,
		));
	}
	
	public static function createTable(PDO $db) {
		$db->exec(<<<sql
			CREATE TABLE tree (
				comId TEXT NOT NULL,
				commonName TEXT,
				scientificName TEXT,
				genus TEXT,
				family TEXT,
				yearPlanted INTEGER,
				lat NUMERIC NOT NULL,
				long NUMERIC NOT NULL
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
	public function parse($csvPath, PDO $db) {
		$handler = function(array $row) use ($db) {	
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
			
			$tree->save($db);
		};
		
		$db->beginTransaction();
		$parser = new CsvParser($csvPath);
		$parser->parseRows($handler);
		$db->commit();
	}
	
}

$data = new DataManager();
$data->prepare();