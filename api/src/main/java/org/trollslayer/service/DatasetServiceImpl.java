package org.trollslayer.service;

import java.io.Writer;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;

import com.opencsv.CSVWriter;
import com.opencsv.bean.StatefulBeanToCsv;
import com.opencsv.bean.StatefulBeanToCsvBuilder;
import com.opencsv.exceptions.CsvDataTypeMismatchException;
import com.opencsv.exceptions.CsvRequiredFieldEmptyException;

import java.io.File;
import java.io.IOException;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.PathVariable;

import org.trollslayer.model.Dataset;
import org.trollslayer.model.Location;

import org.trollslayer.repository.DatasetRepository;
import org.trollslayer.repository.LocationRepository;
import org.trollslayer.exception.ResourceNotFoundException;


@Service
public class DatasetServiceImpl implements DatasetService {
	
    @Autowired
    DatasetRepository datasetRepository;
    
    @Autowired
    LocationRepository locationRepository;
    
    @Override
    public Dataset saveDataset(Dataset dataset) {
    	return datasetRepository.save(dataset);
    }

	@Override
	public List<Dataset> getDatasets() {
		return datasetRepository.findAll();
	}
	
	@Override
	public Dataset getDatasetById(@PathVariable(value = "id") Long datasetId) {
		return datasetRepository.findById(datasetId)
				.orElseThrow(() -> new ResourceNotFoundException("Dataset", "id", datasetId));
	}
	
	@Override
	public List<Dataset> getDatasetsByUserId(String userId) {
		return datasetRepository.getDatasetsByUserId(userId);
	}
	
	// @TODO Function for Dataset Async
	public Callable<String> generateDatasetAsync(Dataset dataset) {
		datasetRepository.save(dataset);
		return new Callable<String>() {

			@Override
			public String call() throws Exception {
				// TODO Auto-generated method stub
				return "OK";
			}
		};
	}
	
	public Dataset generateDataset(Dataset dataset) throws IOException, CsvDataTypeMismatchException, CsvRequiredFieldEmptyException {
	   	 List<Location> listLoc = new ArrayList<Location>(); 
	   	 listLoc = locationRepository.getLocationsByLongLatR(dataset.getLongitude(), dataset.getLatitude(), dataset.getRadius());
	   	 String dataset_formatted_id = String.format("%05d", dataset.getId());
	   	 String filePath = "/tmp/"+dataset_formatted_id+"_"+Instant.now().toEpochMilli()+".csv";
	   	 
	   	 try (
	   			 Writer writer = Files.newBufferedWriter(Paths.get(filePath));
	   	 
	   			 CSVWriter csvWriter = new CSVWriter(writer,
	                CSVWriter.DEFAULT_SEPARATOR,
	                CSVWriter.NO_QUOTE_CHARACTER,
	                CSVWriter.DEFAULT_ESCAPE_CHARACTER,
	                CSVWriter.DEFAULT_LINE_END); ){
	   	 
	   		 StatefulBeanToCsv<Location> beanToCsv = new StatefulBeanToCsvBuilder<Location>(writer)
	   				 .withQuotechar(CSVWriter.NO_QUOTE_CHARACTER).build();
	   		 
	   		 beanToCsv.write(listLoc);
	   	 };
	   	 
	   	 dataset.setFilePath(filePath);;
	   	 
	   	 return dataset;	
	}
	
	public File getFileFromFileSystem(String filePath) throws IOException {
		File file = new File(filePath);
		return file;	
	}
	
	
	public Dataset getDatasetByHash(String fileHash) { 
		return datasetRepository.getDatasetByHash(fileHash); }
	 

	public String getFileFor(String fileHash) {
		Dataset dataset = getDatasetByHash(fileHash);
		String filePath = dataset.getFilePath();
		return filePath;
	}
}
