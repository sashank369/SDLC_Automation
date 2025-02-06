package com.example.demo.controller;

import com.example.demo.entity.Teacher;
import com.example.demo.service.TeacherService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/teacher")
public class TeacherController {

    @Autowired
    private TeacherService teacherService;

    @PostMapping("/{teacher_id}/{sub_id}")
    public ResponseEntity<Teacher> addSubjectToTeacher(@PathVariable Integer teacher_id, @PathVariable Integer sub_id) {
        Teacher updatedTeacher = teacherService.addSubjectToTeacher(teacher_id, sub_id);
        if (updatedTeacher != null) {
            return ResponseEntity.ok(updatedTeacher);
        }
        return ResponseEntity.notFound().build();
    }

    @GetMapping("/{teacher_id}")
    public ResponseEntity<Teacher> getTeacherById(@PathVariable Integer teacher_id) {
        Optional<Teacher> teacherOptional = teacherService.getTeacherById(teacher_id);
        return teacherOptional.map(ResponseEntity::ok).orElseGet(() -> ResponseEntity.notFound().build());
    }

    @GetMapping("/{email}")
    public ResponseEntity<Teacher> getTeacherByEmail(@PathVariable String email) {
        Optional<Teacher> teacherOptional = teacherService.getTeacherByEmail(email);
        return teacherOptional.map(ResponseEntity::ok).orElseGet(() -> ResponseEntity.notFound().build());
    }

    @GetMapping("/allTeachers")
    public List<Teacher> getAllTeachers() {
        return teacherService.getAllTeachers();
    }
}