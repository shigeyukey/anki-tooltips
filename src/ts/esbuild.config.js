// Anki Tooltips
// Copyright (C) Matthias Metelka (kleinerpirat) 2023 <https://github.com/kleinerpirat>
// Copyright (C) Shigeyuki 2025 <http://patreon.com/Shigeyuki>

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.

// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

const { build } = require("esbuild");
const sveltePreprocess = require("svelte-preprocess");
const sveltePlugin = require("esbuild-svelte");
const sassPlugin = require("esbuild-sass-plugin").default;

const production = process.env.NODE_ENV === "production";
const development = process.env.NODE_ENV === "development";

const watch = development
    ? {
        onRebuild(error) {
            console.timeLog;

            if (error) {
                console.error(
                    new Date(),
                    "esbuild: build failed:",
                    error.getMessage(),
                );
            } else {
                console.log(new Date(), "esbuild: build succeeded");
            }
        },
    }
    : false;

const entryPoints = ["src/editor/index.ts", "src/template/index.ts"];

const options = {
    entryPoints,
    outdir: "../../dist/web",
    format: "iife",
    target: "es2018",
    bundle: true,
    minify: production,
    treeShaking: production,
    sourcemap: !production,
    pure: production ? ["console.log", "console.time", "console.timeEnd"] : [],
    watch,
    external: ["svelte", "anki"],
    plugins: [
        sveltePlugin({
            preprocess: sveltePreprocess({
                scss: {
                    includePaths: ["anki/sass"],
                },
            }),
        }),
        sassPlugin(),
    ],
    loader: {
        ".png": "dataurl",
        ".svg": "text",
    },
};

build(options).catch((err) => {
    console.error(err);
    process.exit(1);
});

if (watch) {
    console.log("Watching for changes...");
}
