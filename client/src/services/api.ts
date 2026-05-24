interface Question {
  id: string;
  question: string;
  difficulty: string;
  date: string;
  choices: Array<{
    letter: string;
    text: string;
  }>;
}

interface Answer {
  answer: string;
  explanation: string;
}

interface CreateQuestionRequest {
  question: string;
  difficulty: string;
  choices: string[];
  answer_letter: string;
  explanation: string;
  date: string;
}

class ApiService {
  private baseURL: string;
  private headers: Record<string, string>;

  constructor(
    baseURL: string = import.meta.env.VITE_API_URL || "http://localhost:8000",
  ) {
    this.baseURL = baseURL;
    this.headers = {
      "Content-Type": "application/json",
    };
  }

  setAuthToken(token: string) {
    this.headers["Authorization"] = `Bearer ${token}`;
  }

  clearAuthToken() {
    delete this.headers["Authorization"];
  }

  // Helper method to reduce boilerplate and handle errors
  private async request<T>(
    endpoint: string,
    options: RequestInit = {},
  ): Promise<T> {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers: {
        ...this.headers,
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json() as Promise<T>;
  }

  async getTodayQuestion(): Promise<Question> {
    return this.request<Question>("/questions/today");
  }

  async getQuestionById(id: string): Promise<Question> {
    return this.request<Question>(`/questions/${id}`);
  }

  async getAnswerByQuestionId(questionId: string): Promise<Answer> {
    return this.request<Answer>(`/answers/${questionId}`);
  }

  async createQuestion(data: CreateQuestionRequest): Promise<Question> {
    return this.request<Question>("/questions", {
      method: "POST",
      body: JSON.stringify(data),
    });
  }
}

export default new ApiService();
export type { Question, Answer, CreateQuestionRequest };
