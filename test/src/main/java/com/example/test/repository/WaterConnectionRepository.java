package com.example.test.repository;

import com.example.test.entity.WaterConnection;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface WaterConnectionRepository extends JpaRepository<WaterConnection, Long> {
    // Custom query methods can be defined here
}