package com.example.demo.dto;

import lombok.Data;
import java.util.List;
import com.fasterxml.jackson.annotation.JsonProperty;

@Data
public class SimulationResponse {
    
    // Tell Jackson to map the JSON key 'final_distribution' 
    // to the Java field 'finalDistribution'
    @JsonProperty("final_distribution") 
    private List<Double> finalDistribution; 

    // Tell Jackson to map the JSON key 'vaR_95' 
    // to the Java field 'vaR95'. (Assuming Python uses vaR_95 as well)
    @JsonProperty("VaR_95") 
    private Double vaR95;

    // Python output should use 'cagr' which matches your Java DTO 'cagr' (camelCase here is fine)
    // If Python uses all lowercase 'cagr', then no annotation is strictly needed, 
    // but adding it ensures reliability.
    @JsonProperty("CAGR") // Adjust based on your Python script's exact output case
    private Double cagr; 
}