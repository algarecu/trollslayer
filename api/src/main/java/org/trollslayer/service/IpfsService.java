package org.trollslayer.service;

import io.ipfs.api.IPFS;
import io.ipfs.api.MerkleNode;
import io.ipfs.api.NamedStreamable;
import io.ipfs.multihash.Multihash;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.logging.Logger;

/**
 * The Class IpfsService.
 */
@Service
public class IpfsService {

    /**
     * Gets IPFS initialized.
     *
     * @return the ipfs
     */
    public IPFS getIpfs() {
        return ipfs;
    }
    
    IPFS ipfs = new IPFS("/ip4/127.0.0.1/tcp/5001");
    
    /** The logger. */
    protected Logger logger = Logger.getLogger(IpfsService.class.getName());
    
    
    /**
     * Put a file to IPFS.
     *
     * @param file is the file
     * @return the string
     * @throws IOException Signals that an I/O exception has occurred.
     */
    public MerkleNode saveFile(File file) throws IOException {
    	logger.info("IpfsService put() invoked: for " + file);
        NamedStreamable.FileWrapper fileWrapper = new NamedStreamable.FileWrapper(file);
        MerkleNode addResult = ipfs.add(fileWrapper).get(0);
        logger.info("IpfsService put() result: " + addResult.toJSONString());
        return addResult;
    }
    
    
    public String putFile(File file) throws IOException {
    	MerkleNode addResult = saveFile(file);
        return addResult.toJSONString();
    }
    
    
    /**
     * Put a byte[] to IPFS.
     *
     * @param file is byte array []
     * @return the string
     * @throws IOException Signals that an I/O exception has occurred.
     */
    public String putByte(String filename, byte[] file) throws IOException {
    	//IPFS ipfs = getIpfs() != null ? getIpfs() : new IPFS("/ip4/127.0.0.1/tcp/5001");
        NamedStreamable.ByteArrayWrapper fileWrapper = new NamedStreamable.ByteArrayWrapper(filename, file);//"hello.txt", "G'day world! IPFS rocks!".getBytes()
        MerkleNode addResult = ipfs.add(fileWrapper).get(0);
        logger.info("IpfsService put() result: " + addResult.toJSONString());
        return addResult.toJSONString();
    }

    /**
     * Gets the file from IPFS.
     *
     * @param hashStr is the hash the file, e.g., Qm... (for SHA-256)
     * @return the byte[]
     * @throws IOException Signals that an I/O exception has occurred.
     */
    public byte[] get(String hashStr) throws IOException {
        Multihash filePointer = Multihash.fromBase58(hashStr);
        byte[] fileContents = ipfs.cat(filePointer);
        logger.info("IpfsService get() for " + hashStr);
        return fileContents;
    }

}