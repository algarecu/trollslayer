package org.trollslayer.service;

import java.util.List;
import org.trollslayer.model.Dataset;


public interface DatasetService {
	public abstract Dataset saveDataset(Dataset dataset);
	public abstract Dataset getDatasetById(Long locationId);
	public abstract List<Dataset> getDatasets();
	public abstract List<Dataset> getDatasetsByUserId(String userId);
}
