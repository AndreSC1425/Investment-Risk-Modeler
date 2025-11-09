package com.example.demo.service;

import com.example.demo.dto.PortfolioRequest;
import com.example.demo.dto.SimulationResponse;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.stream.Collectors;

@Service
public class PythonExecutionService {
    private static final String PYTHON_EXECUTABLE_PATH = "C:\\Users\\andre\\PortfolioDeconstructor\\python\\venv\\Scripts\\python.exe";
    private static final String PYTHON_SCRIPT_PATH = "C:\\Users\\andre\\PortfolioDeconstructor\\python\\monte_carlo.py";

    public SimulationResponse runSimulation(PortfolioRequest request) throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        String requestJson = mapper.writeValueAsString(request);

        ProcessBuilder pb = new ProcessBuilder(
                PYTHON_EXECUTABLE_PATH,
                PYTHON_SCRIPT_PATH);

        Process p = pb.start();

        // Write the JSON request to the Python script's standard input
        try (OutputStreamWriter writer = new OutputStreamWriter(p.getOutputStream())) {
            writer.write(requestJson);
        }

        // Read the JSON response from the Python script's standard output
        String pythonOutput = new BufferedReader(new InputStreamReader(p.getInputStream()))
                .lines().collect(Collectors.joining("\n"));

        String errorOutput = new BufferedReader(new InputStreamReader(p.getErrorStream()))
                .lines().collect(Collectors.joining("\n"));

        int exitCode = p.waitFor();

        if (exitCode != 0) {
            throw new RuntimeException("Python script failed with error:\n" + errorOutput);
        }
        // .lines().collect(Collectors.joining("\n"));
        // throw new RuntimeException("Python script failed with error:\n" +
        // errorOutput);
        // }

        int jsonStart = pythonOutput.indexOf('{');

        if (jsonStart == -1) {
            throw new RuntimeException("Python script returned non-JSON data: "
                    + pythonOutput.substring(0, Math.min(pythonOutput.length(), 200)));
        }

        String cleanJsonOutput = pythonOutput.substring(jsonStart).trim();

        return mapper.readValue(cleanJsonOutput, SimulationResponse.class);
    }
}