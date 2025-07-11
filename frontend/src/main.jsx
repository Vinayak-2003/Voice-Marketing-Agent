// frontend/src/main.jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import App from './App.jsx'
import './assets/index.css'

import DashboardPage from './pages/DashboardPage.jsx'
import AgentsPage from './pages/AgentsPage.jsx'
import AgentDetailPage from './pages/AgentDetailPage.jsx'

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        index: true, // This makes it the default child route
        element: <DashboardPage />,
      },
      {
        path: "agents",
        element: <AgentsPage />,
      },
      {
        path: "agents/:agentId",
        element: <AgentDetailPage />,
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)