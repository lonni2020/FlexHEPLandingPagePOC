# FlexHEP Implementation Plan

## 1. Initialize Project

- Create the app from `nathanlonghurst/fast-template`.
- Preserve its FastAPI layered architecture.
- Add a React/Vite frontend.
- Remove PostgreSQL, Docker database services, and 1Password workflows.
- Configure secrets through a local `.env` file.
- Add `.env.example` without real secrets.
- put backend in a backend folder and frontend in a frontend folder like flexhep-frontend

## 2. Configure SQLite

- Replace PostgreSQL settings with SQLite configuration.
- Use an async SQLite connection through SQLAlchemy and `aiosqlite`.
- Store the database at `backend/data/flexhep.db`.
- Ensure the data directory is created automatically.
- Keep the database file out of version control.

## 3. Create Waitlist Backend

- Add a `WaitlistSignup` model containing:
  - `id`
  - `email`
  - `created_at`
- Add a unique constraint on `email`.
- Add request and response schemas.
- Implement the template's DAO, service, and API layers.
- Add `POST /api/v1/waitlist`.
- Validate email format.
- Return a successful response for new emails.
- Return a friendly duplicate response for existing emails.
- Store no information beyond the email and signup timestamp.

## 4. Build Landing Page

- Create a single-page React experience with no multi-page navigation.
- Use a modern, clean, active visual style.
- Use a deep navy, mint, and warm neutral color palette.
- Add strong typography, rounded cards, subtle motion, and responsive layouts.
- Add an original product visual showing a FlexHEP exercise-plan interface rather than relying on a generic stock image.

## 5. Landing Page Content

- Brand: `FlexHEP`
- Headline: `Better home care. Stronger outcomes.`
- Supporting copy focused directly on the visitor and their patients.
- Prominent CTA: `Keep me updated`
- Email field with clear validation and accessible labels.
- Privacy reassurance explaining that the email is only used for FlexHEP updates.

## 6. Three Information Sections

- **Plans that fit the person**
  - Personalize exercises, reps, frequency, and instructions.
- **A shared brain for PTs**
  - Share exercises and consult with other physical therapists.
- **Works wherever your patient is**
  - Use the web experience or print individualized plans as PDFs.

## 7. Thank-You State

- Submit the form asynchronously without navigation.
- Replace the CTA form with a responsive thank-you panel.
- Show `You're on the list.`
- Confirm that the visitor will hear when FlexHEP is ready.
- Handle loading, invalid email, duplicate email, and server errors.

## 8. Frontend and Backend Integration

- Configure Vite to proxy API requests to FastAPI during development.
- Configure FastAPI to serve the built React frontend for production.
- Add CORS configuration only where needed for local development.
- Add a health-check endpoint for local verification.

## 9. Testing

- Add backend tests for valid signup, invalid email, duplicate email, and SQLite persistence.
- Add frontend tests for form submission, loading state, error state, and thank-you state.
- Verify mobile, tablet, and desktop layouts.
- Run the production frontend build.
- Run the FastAPI test suite.
- Confirm the SQLite database is created and populated correctly.

## Scope Note

No email provider, confirmation email, or external mailing service will be implemented. The waitlist will only store the visitor's email and signup timestamp in SQLite.
