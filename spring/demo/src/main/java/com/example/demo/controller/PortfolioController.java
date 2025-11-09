package com.example.demo.controller;

import com.example.demo.dto.PortfolioRequest;
import com.example.demo.dto.SimulationResponse;
import com.example.demo.service.PythonExecutionService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController 
@RequestMapping("/api/portfolio") 
@RequiredArgsConstructor 
@CrossOrigin(origins = "http://localhost:4200") 
public class PortfolioController {

    private final PythonExecutionService pythonExecutionService;

    @PostMapping("/simulate")
    public ResponseEntity<SimulationResponse> runSimulation(@RequestBody PortfolioRequest request) {
        try {
            SimulationResponse response = pythonExecutionService.runSimulation(request);
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            System.err.println("Error running simulation: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .build();
        }
    }
}