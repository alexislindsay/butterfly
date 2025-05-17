import React from "react";

export function ScrollArea({ children, className = "", ...props }) {
  return (
    <div
      className={`overflow-y-auto h-full ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}
