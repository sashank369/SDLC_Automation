package com.example.newdemo.service;

import com.example.newdemo.entity.User;
import com.example.newdemo.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private BCryptPasswordEncoder passwordEncoder;

    public User registerUser(String email, String password, String confirmPassword, boolean agreeToTerms, boolean promotionalEmails, boolean thirdPartySharing) {
        if (!password.equals(confirmPassword)) {
            throw new IllegalArgumentException("Passwords do not match.");
        }

        String passwordHash = passwordEncoder.encode(password);

        User user = new User();
        user.setEmail(email);
        user.setPasswordHash(passwordHash);
        user.setAgreeToTerms(agreeToTerms);
        user.setPromotionalEmails(promotionalEmails);
        user.setThirdPartySharing(thirdPartySharing);

        return userRepository.save(user);
    }

    public boolean validateFields(String email, String phoneNumber) {
        Optional<User> userByEmail = userRepository.findByEmail(email);
        Optional<User> userByPhone = userRepository.findByPhoneNumber(phoneNumber);

        return userByEmail.isEmpty() && userByPhone.isEmpty();
    }

    // Other service methods...
}