package com.example.test.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "water_connection_entity")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class WaterConnection {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "application_no")
    private String applicationNo;

    @Column(name = "application_status")
    private String applicationStatus;

    @Column(name = "connection_category")
    private String connectionCategory;

    @Column(name = "connection_type")
    private String connectionType;

    @Column(name = "connection_holders")
    private String connectionHolders;

    // other fields as necessary
}