package com.example.newdemo.controller;

import com.example.newdemo.entity.User;
import com.example.newdemo.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/register")
public class UserController {

    @Autowired
    private UserService userService;

    @PostMapping
    public ResponseEntity<Object> registerUser(@RequestBody Map<String, Object> payload) {
        String email = (String) payload.get("email");
        String password = (String) payload.get("password");
        String confirmPassword = (String) payload.get("confirmPassword");
        boolean agreeToTerms = (boolean) payload.get("agreeToTerms");
        boolean promotionalEmails = (boolean) payload.get("promotionalEmails");
        boolean thirdPartySharing = (boolean) payload.get("thirdPartySharing");

        try {
            User user = userService.registerUser(email, password, confirmPassword, agreeToTerms, promotionalEmails, thirdPartySharing);
            Map<String, Object> response = new HashMap<>();
            response.put("message", "User registered successfully");
            response.put("user", user);
            return new ResponseEntity<>(response, HttpStatus.CREATED);
        } catch (IllegalArgumentException e) {
            return new ResponseEntity<>(new HashMap<String, Object>() {{ put("message", e.getMessage()); }}, HttpStatus.BAD_REQUEST);
        }
    }

    @GetMapping("/validation")
    public ResponseEntity<Object> validateFields(@RequestParam String email, @RequestParam String phoneNumber) {
        boolean isValid = userService.validateFields(email, phoneNumber);
        Map<String, Object> response = new HashMap<>();

        if (isValid) {
            response.put("message", "Validation successful");
        } else {
            response.put("message", "Email or phone number already exists");
        }

        return new ResponseEntity<>(response, HttpStatus.OK);
    }

    // Other controller methods...
}