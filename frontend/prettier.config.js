/** @type {import("prettier").Config} */
export default {
    plugins: ["prettier-plugin-astro"],
    htmlWhitespaceSensitivity: "ignore",
    tabWidth: 4,
    overrides: [{ files: "*.astro", options: { parser: "astro" } }],
};
