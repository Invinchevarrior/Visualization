export function replaceSvg()
{
    const svgs=document.querySelectorAll(".replace-svg");
    for(let i=0;i<svgs.length;i++)
    {
        const svgName=svgs[i].getAttribute("name");
        const svgPath=`/resource/svg/${svgName}.svg`;

        // 异步请求代码，使用Fetch API
        fetch(svgPath)
        .then(response => response.text())
        .then(svgContent => {
          svgs[i].outerHTML = svgContent;
        })
        .catch(error => console.error(`Error loading SVG: ${error}`));

        // // 同步请求代码，使用XMLHttpRequest
        // const xhr = new XMLHttpRequest();
        // xhr.open('GET', svgPath, false);

        // try {
        //     xhr.send();
        //     if (xhr.status === 200) {
        //         svgs[i].outerHTML = xhr.responseText;
        //     }
        //     else {
        //         console.error(`Error loading SVG: Network request failed with status ${xhr.status}`);
        //     }
        // }
        // catch (error) {
        //     console.error(`Error loading SVG: ${error.message}`);
        // }
    }
}