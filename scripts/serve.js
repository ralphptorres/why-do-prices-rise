import { serve } from "https://deno.land/std@0.208.0/http/server.ts";
import { serveDir } from "https://deno.land/std@0.208.0/http/file_server.ts";

const PORT = 3000;

console.log(`Serving frontend at http://localhost:${PORT}`);

serve(
  (req) => serveDir(req, { fsRoot: "./frontend", urlRoot: "" }),
  { port: PORT }
);
