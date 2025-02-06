package com.example.demo.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "teacher_entity")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class Teacher {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    
    private String name;
    
    @Column(unique = true)
    private String email;
    
    @Column(name = "sub_id")
    private Integer subjectId;
    
    private String address;
    private Integer age;
    private Integer exp;
    private String qualification;
    private String password;
}