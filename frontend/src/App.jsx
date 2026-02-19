import "./styles/global.css";
import { useState } from "react";
import Navbar from "./components/Navbar";
import AdvisorPage from "./pages/AdvisorPage";
import PricingPage from "./pages/PricingPage";
import TrendsPage from "./pages/TrendsPage";

const PAGES = { advisor: AdvisorPage, pricing: PricingPage, trends: TrendsPage };

export default function App() {
  const [page, setPage] = useState("advisor");
  const Page = PAGES[page];

  return (
    <div className="app">
      <Navbar page={page} setPage={setPage} />
      <Page />
    </div>
  );
}