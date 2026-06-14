import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { User, Organization, AuthTokens } from "@/lib/api";

interface AuthState {
  user: User | null;
  organization: Organization | null;
  tokens: AuthTokens | null;
  isAuthenticated: boolean;
  setAuth: (user: User, organization: Organization, tokens: AuthTokens) => void;
  setOrganization: (organization: Organization) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      organization: null,
      tokens: null,
      isAuthenticated: false,
      setAuth: (user, organization, tokens) =>
        set({ user, organization, tokens, isAuthenticated: true }),
      setOrganization: (organization) => set({ organization }),
      logout: () =>
        set({ user: null, organization: null, tokens: null, isAuthenticated: false }),
    }),
    { name: "crm-auth" }
  )
);

interface ThemeState {
  theme: "light" | "dark";
  toggleTheme: () => void;
  setTheme: (theme: "light" | "dark") => void;
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set, get) => ({
      theme: "light",
      toggleTheme: () => set({ theme: get().theme === "light" ? "dark" : "light" }),
      setTheme: (theme) => set({ theme }),
    }),
    { name: "crm-theme" }
  )
);

interface SidebarState {
  isOpen: boolean;
  toggle: () => void;
  setOpen: (open: boolean) => void;
}

export const useSidebarStore = create<SidebarState>((set) => ({
  isOpen: true,
  toggle: () => set((s) => ({ isOpen: !s.isOpen })),
  setOpen: (open) => set({ isOpen: open }),
}));
