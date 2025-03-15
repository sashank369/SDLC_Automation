package com.example.test.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "water_connection_request_entity")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class WaterConnectionRequest {
    private RequestInfo requestInfo;
    private WaterConnection waterConnection;
    private boolean disconnectRequest;
    private boolean isCreateCall;
    private boolean isOldDataEncryptionRequest;
}