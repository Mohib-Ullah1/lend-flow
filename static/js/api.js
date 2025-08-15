// ============================================
// LENDFLOW — API Client
// ============================================

const API_BASE = 'http://localhost:8000/api/v1';

const api = {
  // --- Token Management ---
  getToken() { return localStorage.getItem('access_token'); },
  getRefresh() { return localStorage.getItem('refresh_token'); },
  setTokens(access, refresh) {
    localStorage.setItem('access_token', access);
    if (refresh) localStorage.setItem('refresh_token', refresh);
  },
  clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
  },
  getUser() {
    const u = localStorage.getItem('user');
    return u ? JSON.parse(u) : null;
  },
  setUser(user) { localStorage.setItem('user', JSON.stringify(user)); },
  isLoggedIn() { return !!this.getToken(); },

  // --- Core Request ---
  async request(method, path, data = null, options = {}) {
    const url = path.startsWith('http') ? path : `${API_BASE}${path}`;
    const headers = { ...(options.headers || {}) };

    if (!options.noAuth) {
      const token = this.getToken();
      if (token) headers['Authorization'] = `Bearer ${token}`;
    }

    if (data && !(data instanceof FormData)) {
      headers['Content-Type'] = 'application/json';
    }

    const config = { method, headers };
    if (data) {
      config.body = data instanceof FormData ? data : JSON.stringify(data);
    }

    let response = await fetch(url, config);

    // Auto-refresh token on 401
    if (response.status === 401 && !options.noRetry) {
      const refreshed = await this.refreshToken();
      if (refreshed) {
        headers['Authorization'] = `Bearer ${this.getToken()}`;
        response = await fetch(url, { ...config, headers });
      } else {
        this.clearTokens();
        window.location.href = '/pages/login.html';
        return null;
      }
    }

    if (response.status === 204) return {};

    const result = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw { status: response.status, data: result };
    }

    return result;
  },

  async refreshToken() {
    const refresh = this.getRefresh();
    if (!refresh) return false;
    try {
      const res = await fetch(`${API_BASE}/auth/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh }),
      });
      if (!res.ok) return false;
      const data = await res.json();
      this.setTokens(data.access, data.refresh || refresh);
      return true;
    } catch { return false; }
  },

  // --- Convenience Methods ---
  get(path, opts) { return this.request('GET', path, null, opts); },
  post(path, data, opts) { return this.request('POST', path, data, opts); },
  patch(path, data, opts) { return this.request('PATCH', path, data, opts); },
  put(path, data, opts) { return this.request('PUT', path, data, opts); },
  delete(path, opts) { return this.request('DELETE', path, null, opts); },

  // --- Auth ---
  async login(username, password) {
    const data = await this.post('/auth/login/', { username, password }, { noAuth: true });
    this.setTokens(data.access, data.refresh);
    const user = await this.get('/auth/profile/');
    this.setUser(user);
    return user;
  },

  async register(userData) {
    const data = await this.post('/auth/register/', userData, { noAuth: true });
    return data;
  },

  async getProfile() {
    return this.get('/auth/profile/');
  },

  async changePassword(oldPassword, newPassword) {
    return this.post('/auth/change-password/', { old_password: oldPassword, new_password: newPassword });
  },

  logout() {
    this.clearTokens();
    window.location.href = '/pages/login.html';
  },

  // --- Borrowers ---
  async getBorrowers(params = '') { return this.get(`/borrowers/${params}`); },
  async getBorrower(id) { return this.get(`/borrowers/${id}/`); },
  async createBorrower(data) { return this.post('/borrowers/', data); },

  // --- Loans ---
  async getLoanProducts(params = '') { return this.get(`/loans/products/${params}`); },
  async getApplications(params = '') { return this.get(`/loans/applications/${params}`); },
  async getApplication(id) { return this.get(`/loans/applications/${id}/`); },
  async createApplication(data) { return this.post('/loans/applications/', data); },
  async approveApplication(id, data) { return this.post(`/loans/applications/${id}/approve/`, data); },
  async rejectApplication(id, data) { return this.post(`/loans/applications/${id}/reject/`, data); },
  async disburseApplication(id) { return this.post(`/loans/applications/${id}/disburse/`); },
  async getLoans(params = '') { return this.get(`/loans/${params}`); },
  async getLoan(id) { return this.get(`/loans/${id}/`); },

  // --- Repayments ---
  async getSchedule(loanId) { return this.get(`/repayments/schedule/?loan_id=${loanId}&page_size=100`); },
  async getPayments(params = '') { return this.get(`/repayments/payments/${params}`); },
  async makePayment(loanId, amount, method = 'ach') {
    return this.post('/repayments/make-payment/', { loan_id: loanId, amount, payment_method: method });
  },

  // --- Scoring ---
  async scoreApplication(applicationId) { return this.post('/scoring/run/', { application_id: applicationId }); },
  async getScores() { return this.get('/scoring/scores/'); },

  // --- KYC ---
  async runKYC(borrowerId) { return this.post('/kyc/run/', { borrower_id: borrowerId }); },

  // --- Notifications ---
  async getNotifications() { return this.get('/notifications/'); },
  async getUnreadCount() { return this.get('/notifications/unread_count/'); },
  async markRead(id) { return this.post(`/notifications/${id}/mark_read/`); },
  async markAllRead() { return this.post('/notifications/mark_all_read/'); },

  // --- Reports ---
  async generateReport(type, format = 'pdf') { return this.post('/reports/generate/', { report_type: type, format }); },
  async getReports() { return this.get('/reports/'); },

  // --- Investors ---
  async getPortfolios() { return this.get('/investors/portfolios/'); },
  async getInvestments() { return this.get('/investors/investments/'); },
  async invest(loanId, amount) { return this.post('/investors/invest/', { loan_id: loanId, amount }); },

  // --- Institutions ---
  async getInstitutions() { return this.get('/institutions/'); },
  async updateInstitution(slug, data) { return this.patch(`/institutions/${slug}/`, data); },

  // --- Ledger ---
  async getGLAccounts() { return this.get('/ledger/accounts/'); },
  async getJournalEntries(params = '') { return this.get(`/ledger/entries/${params}`); },

  // --- Documents ---
  async getDocuments(borrowerId = '') {
    const q = borrowerId ? `?borrower_id=${borrowerId}` : '';
    return this.get(`/documents/${q}`);
  },
  async uploadDocument(formData) { return this.request('POST', '/documents/', formData); },

  // --- Audit ---
  async getAuditLogs(params = '') { return this.get(`/audit/${params}`); },
};

// Export for use
window.api = api;
