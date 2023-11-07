import React from "react";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogActions from "@mui/material/DialogActions";
import SettingsIcon from "@mui/icons-material/Settings";
import TextField from "@mui/material/TextField";
import IconButton from "@mui/material/IconButton";
import Button from "@mui/material/Button";
import Grid from "@mui/material/Grid";
import { createDockerDesktopClient } from "@docker/extension-api-client";

const Setting = () => {
  const [open, setOpen] = React.useState(true);
  const [telegramToken, setTelegramToken] = React.useState<string>('');
  const [telegramAllowedIds, setTelegramAllowedIds] = React.useState<string>('');
  const [openaiEndpoint, setOpenaiEndpoint] = React.useState<string>('');
  const [openaiApiKey, setOpenaiApiKey] = React.useState<string>('');

  // if all varaible telegramToken, telegramAllowedIds, openaiEndpoint, openaiApiKey are null, then open the dialog
  React.useEffect(() => {
    if (
      telegramToken === '' ||
      telegramAllowedIds === '' ||
      openaiEndpoint === '' ||
      openaiApiKey === ''
    ) {
      setOpen(true);
    }
  }, [telegramToken, telegramAllowedIds, openaiEndpoint, openaiApiKey]);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    // not allow to close the dialog if any of the variable is null
    if (
      telegramToken === '' ||
      telegramAllowedIds === '' ||
      openaiEndpoint === '' ||
      openaiApiKey === '' 
    ) {
      return;
    }
    setOpen(false);
  };

  const handleSave = async () => {
    // not allow to save the dialog if any of the variable is null
    if (
      telegramToken === '' ||
      telegramAllowedIds === '' ||
      openaiEndpoint === '' ||
      openaiApiKey === ''
    ) {
      return;
    }
    const client = createDockerDesktopClient();
    await client.extension.vm?.service?.post(
      "/credentials",
      JSON.stringify({
        token: telegramToken,
        allowed_ids: telegramAllowedIds,
        openai_endpoint: openaiEndpoint,
        openai_api_key: openaiApiKey,
      })
    );
    setOpen(false);
  };

  return (
    <div>
      <IconButton aria-label="settings" onClick={handleClickOpen}>
        <SettingsIcon />
      </IconButton>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Settings</DialogTitle>
        <DialogContent>
          <DialogContentText mb={2}>
            Please enter your Telegram Bot credentials and OpenAI API key.
          </DialogContentText>
          <Grid
            container
            spacing={1}
            direction="column"
            alignItems="center"
            justifyContent="center"
          >
            <Grid item xs={12}>
              <TextField
                label="Telegram Token"
                sx={{ width: 480 }}
                value={telegramToken ?? ""}
                onChange={(e) => setTelegramToken(e.target.value)}
                type="password"
                required
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Telegram Allowed IDs"
                sx={{ width: 480 }}
                value={telegramAllowedIds ?? ""}
                onChange={(e) => setTelegramAllowedIds(e.target.value)}
                required
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="OpenAI Endpoint"
                sx={{ width: 480 }}
                value={openaiEndpoint ?? ""}
                onChange={(e) => setOpenaiEndpoint(e.target.value)}
                type="password"
                required
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="OpenAI API Key"
                sx={{ width: 480 }}
                value={openaiApiKey ?? ""}
                onChange={(e) => setOpenaiApiKey(e.target.value)}
                type="password"
                required
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleSave}>Save</Button>
          <Button onClick={handleClose}>Cancel</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default Setting;
