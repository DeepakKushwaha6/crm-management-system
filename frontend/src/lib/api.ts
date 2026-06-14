const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

interface RequestOptions extends RequestInit {
  token?: string;
  orgId?: string;
}

class ApiClient {
  private getHeaders(options: RequestOptions = {}): HeadersInit {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };
    if (options.token) {
      headers["Authorization"] = `Bearer ${options.token}`;
    }
    if (options.orgId) {
      headers["X-Organization-ID"] = options.orgId;
    }
    return headers;
  }

  async request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
    const { token, orgId, ...fetchOptions } = options;
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...fetchOptions,
      headers: {
        ...this.getHeaders({ token, orgId }),
        ...(fetchOptions.headers as Record<string, string>),
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: "Request failed" }));
      throw new Error(error.message || error.error || `HTTP ${response.status}`);
    }

    const contentType = response.headers.get("content-type");
    if (contentType?.includes("application/json")) {
      return response.json();
    }
    return response.text() as unknown as T;
  }

  get<T>(endpoint: string, options?: RequestOptions) {
    return this.request<T>(endpoint, { ...options, method: "GET" });
  }

  post<T>(endpoint: string, data?: unknown, options?: RequestOptions) {
    return this.request<T>(endpoint, {
      ...options,
      method: "POST",
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  patch<T>(endpoint: string, data?: unknown, options?: RequestOptions) {
    return this.request<T>(endpoint, {
      ...options,
      method: "PATCH",
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  delete<T>(endpoint: string, options?: RequestOptions) {
    return this.request<T>(endpoint, { ...options, method: "DELETE" });
  }
}

export const api = new ApiClient();

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  role?: string;
  current_organization?: Organization;
}

export interface Organization {
  id: string;
  name: string;
  slug: string;
  plan: string;
}

export interface Membership {
  id: string;
  role: string;
  organization: Organization;
}

export interface Lead {
  id: string;
  first_name: string;
  last_name: string;
  full_name: string;
  email: string;
  phone: string;
  company: string;
  source: string;
  status: string;
  score: number;
  created_at: string;
}

export interface Customer {
  id: string;
  name: string;
  email: string;
  phone: string;
  company: string;
  status: string;
  churn_risk: number;
  lifetime_value: string;
  created_at: string;
}

export interface Opportunity {
  id: string;
  title: string;
  stage: string;
  amount: string;
  probability: number;
  expected_close_date: string | null;
  customer_name?: string;
}

export interface Task {
  id: string;
  title: string;
  description: string;
  priority: string;
  status: string;
  due_date: string | null;
}

export interface DashboardData {
  revenue: { total: number; monthly: number; pipeline_value: number };
  sales: {
    total_leads: number;
    converted_leads: number;
    open_opportunities: number;
    won_deals: number;
    lost_deals: number;
  };
  conversion: { lead_conversion_rate: number; win_rate: number };
  customers: { total: number; active: number; at_risk: number };
  tasks: { pending: number; overdue: number; completed_this_month: number };
  recent_activities: Array<{
    id: string;
    activity_type: string;
    subject: string;
    created_at: string;
    user__email: string;
  }>;
}

export const authApi = {
  register: (data: {
    email: string;
    password: string;
    first_name: string;
    last_name: string;
    organization_name: string;
  }) => api.post<{ user: User; organization: Organization; tokens: AuthTokens }>("/auth/register/", data),

  login: (data: { email: string; password: string }) =>
    api.post<{ user: User; memberships: Membership[]; tokens: AuthTokens }>("/auth/login/", data),

  logout: (refresh: string, token: string, orgId: string) =>
    api.post("/auth/logout/", { refresh }, { token, orgId }),

  me: (token: string, orgId: string) => api.get<User>("/auth/me/", { token, orgId }),
};

export const crmApi = {
  getDashboard: (token: string, orgId: string) =>
    api.get<DashboardData>("/dashboard/", { token, orgId }),

  getLeads: (token: string, orgId: string, params?: string) =>
    api.get<PaginatedResponse<Lead>>(`/leads/${params ? `?${params}` : ""}`, { token, orgId }),

  createLead: (token: string, orgId: string, data: Partial<Lead>) =>
    api.post<Lead>("/leads/", data, { token, orgId }),

  getCustomers: (token: string, orgId: string) =>
    api.get<PaginatedResponse<Customer>>("/customers/", { token, orgId }),

  getOpportunities: (token: string, orgId: string) =>
    api.get<PaginatedResponse<Opportunity>>("/opportunities/", { token, orgId }),

  getPipeline: (token: string, orgId: string) =>
    api.get<Record<string, { count: number; total_amount: number; opportunities: Opportunity[] }>>(
      "/opportunities/pipeline/",
      { token, orgId }
    ),

  updateOpportunityStage: (token: string, orgId: string, id: string, stage: string) =>
    api.patch<Opportunity>(`/opportunities/${id}/stage/`, { stage }, { token, orgId }),

  getTasks: (token: string, orgId: string) =>
    api.get<PaginatedResponse<Task>>("/tasks/", { token, orgId }),

  getRevenueAnalytics: (token: string, orgId: string) =>
    api.get<{ data: Array<{ period: string; revenue: number }> }>("/analytics/revenue/", { token, orgId }),

  getPipelineAnalytics: (token: string, orgId: string) =>
    api.get<{ funnel: Array<{ stage: string; count: number; value: number }> }>(
      "/analytics/pipeline/",
      { token, orgId }
    ),

  getTeamPerformance: (token: string, orgId: string) =>
    api.get<{ team: Array<{ name: string; role: string; deals_won: number; revenue: number }> }>(
      "/analytics/team/",
      { token, orgId }
    ),
};

export const aiApi = {
  scoreLead: (token: string, orgId: string, leadId: string) =>
    api.post("/ai/lead-score/", { lead_id: leadId }, { token, orgId }),

  predictChurn: (token: string, orgId: string, customerId: string) =>
    api.post("/ai/churn-predict/", { customer_id: customerId }, { token, orgId }),

  forecastRevenue: (token: string, orgId: string, period: string) =>
    api.post<{ forecasts: Array<{ period: string; forecasted_revenue: number; confidence: number }>; period_type: string }>(
      "/ai/revenue-forecast/",
      { period },
      { token, orgId }
    ),

  generateEmail: (token: string, orgId: string, type: string, context: Record<string, string>) =>
    api.post<{ subject: string; body: string; type: string }>("/ai/generate-email/", { type, context }, { token, orgId }),

  analyzeSentiment: (token: string, orgId: string, text: string) =>
    api.post<{ sentiment: string; score: number; confidence: number }>(
      "/ai/sentiment/",
      { text },
      { token, orgId }
    ),

  followUp: (token: string, orgId: string, data: Record<string, unknown>) =>
    api.post<{ recommended_action: string; best_channel: string; timing_days: number; urgency: string }>(
      "/ai/follow-up/",
      data,
      { token, orgId }
    ),
};

export const notificationsApi = {
  getAll: (token: string, orgId: string) =>
    api.get<PaginatedResponse<{ id: string; title: string; message: string; is_read: boolean; notification_type: string }>>(
      "/notifications/",
      { token, orgId }
    ),
};
