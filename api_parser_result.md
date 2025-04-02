api parser result: # Implementation Requirements

## API Tag: User Registration

### 1. Endpoint: `/api/v1/register` - Register a new user

#### Controller Layer
- **Task**: Implement `registerUser` POST method.
- **Request Body**:
  - `email`: string, format email, required
  - `password`: string, min length 8, required
  - `confirmPassword`: string, required
  - `agreeToTerms`: boolean, required
  - `promotionalEmails`: boolean
  - `thirdPartySharing`: boolean

#### Service Layer
- **Method**: `registerUser(email, password, confirmPassword, agreeToTerms, promotionalEmails, thirdPartySharing)`
- **Logic**: Validate input, check password confirmation, hash password, save user details.

#### Repository Layer
- **Entity**: `User`
  - Attributes:
    - `userId`: string
    - `email`: string
    - `passwordHash`: string
    - `agreeToTerms`: boolean
    - `promotionalEmails`: boolean
    - `thirdPartySharing`: boolean

### 2. Endpoint: `/api/v1/register/validation` - Validate email and phone number

#### Controller Layer
- **Task**: Implement `validateFields` GET method.
- **Query Parameters**:
  - `email`: string, format email
  - `phoneNumber`: string

#### Service Layer
- **Method**: `validateFields(email, phoneNumber)`
- **Logic**: Validate email format, check if email or phone number exists in the database.

### 3. Endpoint: `/api/v1/register/socialmedia` - Register a user with social media

#### Controller Layer
- **Task**: Implement `registerSocialMediaUser` POST method.
- **Request Body**:
  - `socialMedia`: string, enum [facebook, google, twitter], required
  - `socialMediaToken`: string, required

#### Service Layer
- **Method**: `registerSocialMediaUser(socialMedia, socialMediaToken)`
- **Logic**: Validate social media token, retrieve user info from social media provider, save user details.

#### Repository Layer
- **Entity**: Extend `User` entity with social media fields if necessary.

### 4. Endpoint: `/api/v1/register/forgotpassword` - Recover forgotten password

#### Controller Layer
- **Task**: Implement `recoverPassword` POST method.
- **Request Body**:
  - `email`: string, format email, required

#### Service Layer
- **Method**: `recoverPassword(email)`
- **Logic**: Check if email exists, generate password recovery link, send email.

### Data Models

- **User**:
  - `userId`: string
  - `email`: string, format email
  - `passwordHash`: string
  - `agreeToTerms`: boolean
  - `promotionalEmails`: boolean
  - `thirdPartySharing`: boolean

- **Responses**:
  - `ErrorResponse`: Contains `message` string
  - `SuccessResponse`: Contains `message` string and `user` object with `userId` and `email`

### Database Schema

- **Table**: `users`
  - `user_id`: VARCHAR, Primary Key
  - `email`: VARCHAR, Unique
  - `password_hash`: VARCHAR
  - `agree_to_terms`: BOOLEAN
  - `promotional_emails`: BOOLEAN
  - `third_party_sharing`: BOOLEAN

This detailed breakdown should guide the development of the Controller, Service, and Repository layers, adhering to the specified API contract.
