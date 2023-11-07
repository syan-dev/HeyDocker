import React from "react";
import Avatar from "@mui/material/Avatar";
import Paper from "@mui/material/Paper";
import { deepOrange, deepPurple } from "@mui/material/colors";
import { Box, Typography } from "@mui/material";


export default function Message(props: any) {
  const { name, text } = props;
  const avatarName = name ? name[0].toUpperCase() : "D";
  const avatarColor = name ? deepOrange[500] : deepPurple[300];
  const avatarStyle = {
    width: 32,
    height: 32,
    backgroundColor: avatarColor,
    marginRight: 1,
  };

  return (
    <Box sx={{ display: "flex", alignItems: "center", my: 1 }}>
      <Avatar sx={avatarStyle} >{avatarName}</Avatar>
      <Paper
        sx={{
          p: 2,
          borderRadius: 2,
          maxWidth: "100%",
        }}
      >
        <Typography variant="body2">{text}</Typography>
      </Paper>
    </Box>
  );
}