# Computer Science Daily Trivia - Frontend

A Vue.js 3 frontend for the Computer Science Daily Trivia application. Built with Vite, TypeScript, Pinia for state management, and Auth0 for authentication.

## Features

- **Auth0 Integration**: Secure authentication with Auth0
- **Daily Trivia Questions**: Fetch and display today's computer science trivia question
- **Multiple Choice**: Interactive multiple-choice interface with real-time feedback
- **Answer Verification**: Instant feedback on answer correctness with explanations
- **Responsive Design**: Mobile-friendly interface with gradient UI
- **State Management**: Centralized state management with Pinia
- **TypeScript**: Full TypeScript support for type safety

## Project Structure

```
src/
├── components/          # Reusable Vue components
│   ├── QuestionCard.vue      # Displays trivia question and choices
│   └── AnswerSection.vue     # Shows answer and explanation
├── services/            # API communication layer
│   └── api.ts               # HTTP client for backend API
├── stores/              # Pinia state management
│   ├── auth.ts              # Auth0 state
│   └── trivia.ts            # Trivia data state
├── router/              # Vue Router configuration
│   └── index.ts             # Route definitions and guards
├── views/               # Full page components
│   ├── HomePage.vue         # Today's trivia question
│   ├── QuestionPage.vue     # Specific question by ID
│   └── CallbackPage.vue     # Auth0 callback handler
├── App.vue              # Root application component
└── main.ts              # Application entry point
```

## Prerequisites

- Node.js 20.19.0 or >=22.12.0
- pnpm (or npm/yarn)
- Auth0 account with an application created
- Running backend API server

## Setup & Configuration

### 1. Environment Variables

Create a `.env.local` file in the project root (copy from `.env.example`):

```env
# Auth0 Configuration
VITE_AUTH0_DOMAIN=your-auth0-domain.auth0.com
VITE_AUTH0_CLIENT_ID=your-auth0-client-id
VITE_AUTH0_AUDIENCE=your-auth0-audience

# API Configuration
VITE_API_URL=http://localhost:8000
```

### 2. Auth0 Setup

1. Go to https://auth0.com and sign up/login
2. Create a new Single Page Application (SPA)
3. In Application Settings:
   - **Allowed Callback URLs**: `http://localhost:5173` (for development)
   - **Allowed Logout URLs**: `http://localhost:5173`
   - **Allowed Web Origins**: `http://localhost:5173`
4. Configure your Auth0 API:
   - Create a new API with your desired identifier (e.g., `https://comp-sci-daily-api`)
   - Set the signing algorithm to `RS256`
5. Configure Auth0 Rules or Actions to add audience to tokens (if needed)

### 3. Dependencies Installation

```bash
pnpm install
```

## Development

### Start Development Server

```bash
pnpm dev
```

The application will be available at `http://localhost:5173`

### Type Checking

```bash
pnpm type-check
```

### Linting

```bash
pnpm lint
```

Format and fix linting issues:

```bash
pnpm format
```

### Run Tests

```bash
pnpm test:unit
```

## Build & Production

### Build for Production

```bash
pnpm build
```

### Preview Production Build Locally

```bash
pnpm preview
```

## Key Components

### QuestionCard Component (`src/components/QuestionCard.vue`)
- Displays the trivia question
- Shows multiple choice options with letters (A, B, C, D)
- Highlights selected answer
- Shows correct/incorrect feedback after revealing answer

### AnswerSection Component (`src/components/AnswerSection.vue`)
- Button to reveal the correct answer
- Displays answer correctness status
- Shows explanation for the answer
- Navigation to next question

### HomePage View (`src/views/HomePage.vue`)
- Main interface for trivia quiz
- Displays today's question
- User profile and logout option

### QuestionPage View (`src/views/QuestionPage.vue`)
- Displays a specific question by ID
- Similar interface to HomePage with navigation

## State Management with Pinia

### Trivia Store (`src/stores/trivia.ts`)
Manages trivia quiz state:
- `currentQuestion`: Currently displayed question
- `currentAnswer`: Answer with explanation
- `selectedChoice`: User's selected answer
- `isAnswerRevealed`: Whether the answer has been revealed
- `isLoading`: Loading state for API calls
- `error`: Error messages

Key actions:
- `fetchTodayQuestion()`: Get today's trivia question
- `fetchQuestionById(id)`: Get a specific question
- `revealAnswer()`: Fetch and display the answer
- `selectChoice(letter)`: Store user's choice
- `reset()`: Clear all state

### Auth Store (`src/stores/auth.ts`)
Manages authentication state:
- `isAuthenticated`: Auth status
- `user`: Logged-in user info
- `isLoading`: Auth loading state

Key actions:
- `login()`: Redirect to Auth0 login
- `logout()`: Log out and clear tokens
- `getAccessToken()`: Get token for API calls

## API Integration

The frontend communicates with the backend API via the `ApiService` class (`src/services/api.ts`):

```typescript
// Get today's question
const question = await apiService.getTodayQuestion()

// Get specific question
const question = await apiService.getQuestionById(id)

// Get answer for a question
const answer = await apiService.getAnswerByQuestionId(questionId)
```

All API calls automatically include the Auth0 access token in the `Authorization` header.

## Authentication Flow

1. User visits the app and is redirected to Auth0 login page
2. After successful login, Auth0 redirects to `/callback`
3. Callback page fetches access token and redirects to home page
4. Access token is stored and automatically included in all API requests
5. On logout, token is cleared and user is logged out of Auth0

## Routing

The application uses Vue Router with the following routes:

- `/` - HomePage (protected) - Today's trivia question
- `/question/:id` - QuestionPage (protected) - Specific question by ID
- `/callback` - CallbackPage (public) - Auth0 callback handler

Routes marked as `protected` require authentication. Unauthenticated users are redirected to Auth0 login.

## Browser Support

Modern browsers with ES2020+ support:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Development Notes

### Adding New Endpoints

1. Add the endpoint to `ApiService` in `src/services/api.ts`
2. Add corresponding actions to the appropriate Pinia store
3. Create/update component to use the new store action

### Component Development

Use the existing components as templates:
- Follow the composition API pattern with `<script setup>`
- Use TypeScript for type safety
- Import stores and computed values from Pinia
- Use scoped styling for component isolation

### Styling

The application uses:
- Gradient background (purple tones)
- Card-based layout
- Smooth transitions and animations
- Responsive design with flexbox/grid

Color scheme:
- Primary: `#667eea` (purple)
- Secondary: `#764ba2` (dark purple)
- Success: `#28a745` (green)
- Error: `#dc3545` (red)

## Troubleshooting

### Auth0 Login Not Working
- Check that your Auth0 domain and client ID are correct in `.env.local`
- Verify Auth0 callback URLs include `http://localhost:5173`
- Check browser console for errors

### API Calls Failing
- Ensure the backend API is running at `VITE_API_URL`
- Verify the access token is being sent correctly
- Check browser Network tab to see the actual requests

### Tokens Expired
- The app should automatically refresh tokens using `getAccessTokenSilently()`
- If not, manually logout and login again

## Recommended IDE Setup

- [VS Code](https://code.visualstudio.com/)
- [Vue - Official](https://marketplace.visualstudio.com/items?itemName=Vue.volar) extension
- [TypeScript Vue Plugin](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin)

## Additional Resources

- [Vue 3 Documentation](https://vuejs.org/)
- [Vite Documentation](https://vite.dev/)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [Auth0 Vue Documentation](https://auth0.com/docs/quickstart/spa/vue)
- [Vue Router Documentation](https://router.vuejs.org/)
