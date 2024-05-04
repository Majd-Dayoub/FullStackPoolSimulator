document.addEventListener('DOMContentLoaded', initializeCueBallInteraction);

function initializeCueBallInteraction() {
    // Fetch the SVG element directly within the function to handle dynamic content updates.
    const svgElement = document.querySelector('.game-container svg');
    if (!svgElement) {
        console.warn('SVG element not found.');
        return; // Exit if SVG element does not exist
    }

    let isDragging = false;
    let line = null;
    let cueBall = document.querySelector('.game-container circle[fill="WHITE"]');
    if (!cueBall) {
        console.warn('Cue ball not found.');
        return; // Exit if cue ball does not exist
    }

    function getMousePosition(evt) {
        let CTM = svgElement.getScreenCTM();
        return {
            x: (evt.clientX - CTM.e) / CTM.a,
            y: (evt.clientY - CTM.f) / CTM.d
        };
    }

    function createLine(x1, y1, x2, y2) {
        let line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('stroke', 'black');
        line.setAttribute('stroke-width', '4');
        svgElement.appendChild(line);
        line.setAttribute('x1', x1);
        line.setAttribute('y1', y1);
        line.setAttribute('x2', x2);
        line.setAttribute('y2', y2);
        return line;
    }

    function finalizeShot(dx, dy) {
        $.ajax({
            url: '/shoot',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ dx, dy }),
            success: function(response) {
                console.log("Shot applied successfully:", response);
                if (response && response.frames) {
                    displayFrames(response.frames);
                    $("#player1Name").text(response.player1Name);
                    $("#player2Name").text(response.player2Name);
                    $("#currentPlayer").text(response.currentPlayer);
                } else {
                    console.error("No frames received:", response);
                }
            },
            error: function(xhr, status, error) {
                console.error("Error applying shot:", error);
                console.log("Status:", status);
                console.log("Response Text:", xhr.responseText);
            }
        });
    }

    cueBall.addEventListener('mousedown', function(evt) {
        isDragging = true;
        const pos = getMousePosition(evt);
        line = createLine(cueBall.cx.baseVal.value, cueBall.cy.baseVal.value, pos.x, pos.y);
    });

    svgElement.addEventListener('mousemove', function(evt) {
        if (isDragging && line) {
            const pos = getMousePosition(evt);
            line.setAttribute('x2', pos.x);
            line.setAttribute('y2', pos.y);
        }
    });

    window.addEventListener('mouseup', function(evt) {
        if (isDragging) {
            isDragging = false;
            const pos = getMousePosition(evt);
            const dx = pos.x - cueBall.cx.baseVal.value;
            const dy = pos.y - cueBall.cy.baseVal.value;
            if (line) svgElement.removeChild(line);
            finalizeShot(dx, dy);
        }
    });
}

function displayFrames(frames) {
    let currentFrame = 0;
    function displayNextFrame() {
        if (currentFrame >= frames.length) {
            console.log("All frames displayed.");
            // Re-initialize the cue ball interaction for the next shot.
            initializeCueBallInteraction();
            return;
        }

        const frameSVG = frames[currentFrame].svg;
        if (frameSVG) {
            $('.game-container').html(frameSVG);
            currentFrame++;
            setTimeout(displayNextFrame, 3); // Adjust the timeout for smoother animation
        } else {
            console.error(`Frame ${currentFrame} does not have valid SVG data.`);
        }
    }
    displayNextFrame();
}
