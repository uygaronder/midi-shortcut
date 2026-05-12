import { useState, useEffect } from 'react';

const useRawInputEvents = () => {
  const [rawEvent, setRawEvent] = useState(null);

  useEffect(() => {
    // Check we're running inside Electron
    if (!window.electronAPI) {
      console.warn('electronAPI not available — are you running in Electron?');
      return;
    }

    // Subscribe to MIDI/input events from main process
    const unsubscribe = window.electronAPI.onRawInputEvent((event) => {
      setRawEvent(event);
    });

    // Cleanup when component unmounts
    return () => unsubscribe();
  }, []);

  return rawEvent;
};

export default useRawInputEvents;