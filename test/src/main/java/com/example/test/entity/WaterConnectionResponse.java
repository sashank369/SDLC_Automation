package com.example.test.entity;

import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class WaterConnectionResponse {
    private String status;
    private String message;
    private WaterConnection waterConnection;
}