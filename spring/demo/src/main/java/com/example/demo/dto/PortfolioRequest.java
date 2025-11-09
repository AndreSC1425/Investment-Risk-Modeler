package com.example.demo.dto;

import lombok.Data;
import java.util.List;
import java.util.Map;

@Data 
public class PortfolioRequest {
    private List<String> tickers; 

    private Map<String, Double> weights; 
    
    private String analysisType; 
}