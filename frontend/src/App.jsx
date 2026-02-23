import "./styles/global.css";
import Navbar from "./components/Navbar";
import AdvisorPage from "./pages/AdvisorPage";
import PricingPage from "./pages/PricingPage";
import TrendsPage from "./pages/TrendsPage";
import LoginPage from "./pages/LoginPage";

import { useEffect, useState } from "react";
import { auth, provider } from "./firebase";
import { signInWithPopup, signOut, onAuthStateChanged } from "firebase/auth";

const PAGES = {
  advisor: AdvisorPage,
  pricing: PricingPage,
  trends: TrendsPage,
};

export default function App() {
  const [page, setPage] = useState("advisor");
  const [user, setUser] = useState(null);

  const Page = PAGES[page];

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
      if (currentUser) {
        const token = await currentUser.getIdToken();
        localStorage.setItem("token", token);
        setUser(currentUser);
      } else {
        localStorage.removeItem("token");
        setUser(null);
      }
    });

    return () => unsubscribe();
  }, []);

  const login = async () => {
    await signInWithPopup(auth, provider);
  };

  const logout = async () => {
    await signOut(auth);
  };

  if (!user) {
    return <LoginPage login={login} />;
  }

  return (
    <div className="app">
      <Navbar
        page={page}
        setPage={setPage}
        user={user}
        logout={logout}
      />
      <Page user={user} />
    </div>
  );
}