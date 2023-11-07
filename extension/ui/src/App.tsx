import React, { useEffect, useRef } from "react";
import Button from "@mui/material/Button";
import { createDockerDesktopClient } from "@docker/extension-api-client";
import {
  Box,
  Container,
  Paper,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import List from "@mui/material/List";
import Setting from "./Setting";
import Message from "./Message";

// Note: This line relies on Docker Desktop's presence as a host application.
// If you're running this React app in a browser, it won't work properly.
const client = createDockerDesktopClient();

function useDockerDesktopClient() {
  return client;
}

export function App() {
  const [messages, setMessages] = React.useState<any>([]);
  const ddClient = useDockerDesktopClient();
  const paperRef = useRef(null);

  const fetchAndDisplayResponse = async () => {
    // const result = await ddClient.extension.vm?.service?.get('/hello');
    const result = (await ddClient.extension.vm?.service?.get("/messages")) as {
      messages: any[];
    };
    setMessages(result.messages.reverse());
  };

  // interval 1s fetch messages
  useEffect(() => {
    const interval = setInterval(() => {
      fetchAndDisplayResponse();
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    // Scroll to the bottom when messages change
    if (paperRef.current) {
      const element = paperRef.current as HTMLElement;
      element.scrollTop = element.scrollHeight;
    }
  }, [messages]);

  return (
    <>
      <Box sx={{ display: "flex", alignItems: "center" }}>
        <Typography variant="h3">HeyDocker</Typography>
        <Setting />
      </Box>
      <Typography variant="body1" color="text.secondary" sx={{ my: 2 }}>
        Empower your Docker workflows and system monitoring with HeyDocker, your
        virtual Docker companion in your chat app. Streamline operations, gain
        insights, and maintain optimal performance effortlessly.
      </Typography>

      {/* // check if messages array empty then don't display */}
      {messages.length > 0 && (
        <Container
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            my: 2,
          }}
        >
          <Paper
            ref={paperRef}
            style={{
              maxHeight: "70vh",
              width: "80vw",
              overflow: "auto",
              backgroundColor: "transparent",
              padding: "10px",
            }}
          >
            <List>
              {messages.map((message: any) => {
                return (
                  <Message name={message.username} text={message.message} />
                );
              })}
            </List>
          </Paper>
        </Container>
      )}
    </>
  );
}
