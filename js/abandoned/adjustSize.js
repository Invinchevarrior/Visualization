export function keepHeight()
{
    const svgs = document.querySelectorAll(".preSvg");

    for (let i = 0; i < svgs.length; i++) {
        const svg = svgs[i].firstElementChild;
        svg.setAttribute("preserveAspectRatio", "xMidYMid");
        // const width = svgs[i].clientWidth;
        // svgs[i].style.height = `${width}px`;
    }
}