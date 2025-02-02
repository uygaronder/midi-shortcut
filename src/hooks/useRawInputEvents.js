// src/hooks/useRawInputEvents.js
import { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';

const useRawInputEvents = () => {
  const [rawEvent, setRawEvent] = useState(null);

  useEffect(() => {
    const socket = io("http://localhost:5000");

    socket.on("connect", () => {
      console.log("Socket.IO connected:", socket.id);
    });

    socket.on("raw_input_event", (data) => {
      console.log("Received raw input event:", data);
      setRawEvent(data);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  return rawEvent;
};

export default useRawInputEvents;
