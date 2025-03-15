package com.example.test.controller;

import com.example.test.entity.WaterConnectionRequest;
import com.example.test.entity.WaterConnectionResponse;
import com.example.test.service.WaterConnectionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/wc")
public class WaterConnectionController {
    @Autowired
    private WaterConnectionService waterConnectionService;

    @PostMapping("/_create")
    public ResponseEntity<WaterConnectionResponse> createWaterConnectionUsingPOST(@RequestBody WaterConnectionRequest request) {
        WaterConnectionResponse response = waterConnectionService.createWaterConnection(request);
        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    // Define other endpoints (_encryptOldData, _plainsearch, _search, _update)
}