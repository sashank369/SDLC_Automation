api parser result: ### User Registration API Implementation Requirements

#### API Tag: User Registration

**Endpoints:**

1. **POST /register**
   - **Summary:** Register a new user.
   - **Request Body:**
     - **email** (string, email, required): User's email address.
     - **password** (string, minLength: 8, required): User's password.
     - **confirmPassword** (string, required): Confirmation of user's password.
     - **agreeToTerms** (boolean, required): User agreement to terms.
     - **promotionalEmails** (boolean): User consent for promotional emails.
     - **thirdPartySharing** (boolean): User consent for third-party data sharing.
   - **Responses:**
     - **201:** User registered successfully.
     - **400:** Validation failed.
     - **500:** Internal server error.

2. **GET /register/validation**
   - **Summary:** Validate email and phone number.
   - **Parameters:**
     - **email** (string, email): User's email address.
     - **phoneNumber** (string): User's phone number.
   - **Responses:**
     - **200:** Validation successful.
     - **400:** Validation failed.

3. **POST /register/socialmedia**
   - **Summary:** Register a new user via social media.
   - **Request Body:**
     - **socialMedia** (string, enum: facebook, google, twitter, required): Social media platform.
     - **socialMediaToken** (string, required): Token from social media.
   - **Responses:**
     - **201:** User registered successfully.
     - **400:** Validation failed.
     - **500:** Internal server error.

4. **POST /register/forgotpassword**
   - **Summary:** Recover forgotten password.
   - **Request Body:**
     - **email** (string, email, required): User's email address.
   - **Responses:**
     - **200:** Password recovery initiated.
     - **400:** Email does not exist.
     - **500:** Internal server error.

**Data Models:**

- **UserRegistrationRequest:**
  - **Attributes:**
    - email: string
    - password: string
    - confirmPassword: string
    - agreeToTerms: boolean
    - promotionalEmails: boolean
    - thirdPartySharing: boolean

- **ValidationResult:**
  - **Attributes:**
    - message: string
    - details: object

- **SocialMediaRegistrationRequest:**
  - **Attributes:**
    - socialMedia: string
    - socialMediaToken: string

- **ForgotPasswordRequest:**
  - **Attributes:**
    - email: string

**Database Schema:**

- **User Table:**
  - id: string (Primary Key)
  - email: string (Unique)
  - passwordHash: string
  - agreeToTerms: boolean
  - promotionalEmails: boolean
  - thirdPartySharing: boolean

**Controller Layer Tasks:**

- Implement `UserRegistrationController` with endpoints for `/register`, `/register/validation`, `/register/socialmedia`, and `/register/forgotpassword`.

**Service Layer Tasks:**

- Implement `UserRegistrationService` with methods:
  - `registerUser(UserRegistrationRequest request)`
  - `validateEmailAndPhone(String email, String phoneNumber)`
  - `registerUserViaSocialMedia(SocialMediaRegistrationRequest request)`
  - `recoverPassword(ForgotPasswordRequest request)`

**Repository Layer Tasks:**

- Implement `UserRepository` for database interactions:
  - `save(User user)`
  - `findByEmail(String email)`
  - `existsByEmail(String email)`

This detailed breakdown ensures each layer's requirements are clear, allowing the development team to proceed with implementation in alignment with the API contract.
