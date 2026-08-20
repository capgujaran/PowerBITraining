import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./globals.css";
import { LearningStudio } from "./learning-studio";

const root = document.getElementById("root");

if (!root) throw new Error("The site root element is missing.");

createRoot(root).render(
  <StrictMode>
    <LearningStudio />
  </StrictMode>,
);
