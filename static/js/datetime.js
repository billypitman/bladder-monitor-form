

// Get the user's timezone offset in minutes
const timezoneOffsetMinutes = new Date().getTimezoneOffset();

// Set the default value of the datetime input field to the current date and time in the user's timezone
const now = new Date();
const localDatetime = new Date(now.getTime() - timezoneOffsetMinutes * 60000);

// Set the default value for timestamp field
const timestampInput = document.getElementById("timestamp");
if (timestampInput) {
  timestampInput.value = localDatetime.toISOString().slice(0, 16);
}