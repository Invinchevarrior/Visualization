import * as svgHandling from "./svgHandling.js";
import * as fileHandling from "./fileHandling.js";

window.addEventListener("load", () => {
    svgHandling.replaceSvg();

    const upload = document.querySelector("#upload-box");
    upload.addEventListener("click", fileHandling.handleUpload);

    const result=document.querySelector("#result-box");
    result.addEventListener("click", fileHandling.fetchAndDisplayFiles);
    //document.getElementById('result-box').addEventListener('click', fileHandling.fetchUploadedFiles);
});