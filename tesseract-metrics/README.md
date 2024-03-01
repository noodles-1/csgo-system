<h1> License Plate Recognition Metrics </h1>
<p> 
    <a href="https://github.com/UB-Mannheim/tesseract/wiki"> Tesseract 5.3.3 </a>
    was used to test 33 
    <a href="https://universe.roboflow.com/2014-series-license-plate/knn-brxiq"> 
        Philippine 2014 License Plates.
    </a>
</p>
<h3> Results </h3>
<table>
    <tr>
        <th> Recall </th>
        <td> 0.6969 (69.69%) </td>
    </tr>
    <tr>
        <th> F1 Score </th>
        <td> 0.8214 (82.14%) </td>
    </tr>
</table>
<h3> Notes </h3>
<p> 
    Text from images were retrieved as a string. Some strings included non-alphanumeric characters along with the predicted license plate number. Testing was done by finding actual license plate string in the predicted license plate, wherein <code> annotation </code> is a list of actual license plate numbers, <code> annotation[i] = license_plate<sub>i</sub> </code> denotes the actual license plate of the <code> i<sup>th</sup> </code> license plate image, <code> predicted[i] </code> denotes the predicted license plate of the <code> i<sup>th</sup> </code> license plate image, and <code> annotation[i] in predicted[i] </code> evaluates to either correct or incorrect inference.
</p>
<p>
    The image was resized to a factor of 3, and gaussian blur was applied to improve recall. Out of 33 images, only 23 images had matching actual license plate number with the predicted license plate string.
</p>