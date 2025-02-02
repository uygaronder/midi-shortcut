// src/contexts/RawInputContext.js
import React, { createContext, useContext } from 'react';

// Create the context with an initial value of null.
const RawInputContext = createContext(null);

// A custom hook for easier access to the context.
export const useRawInput = () => useContext(RawInputContext);

export const RawInputProvider = ({ value, children }) => {
  return (
    <RawInputContext.Provider value={value}>
      {children}
    </RawInputContext.Provider>
  );
};