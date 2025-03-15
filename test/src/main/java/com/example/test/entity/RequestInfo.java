package com.example.test.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "request_info_entity")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class RequestInfo {
    private String requestId;
    private String requestTimestamp;
    // other fields as necessary
}