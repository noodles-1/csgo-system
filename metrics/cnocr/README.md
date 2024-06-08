<h1> License Plate Recognition Metrics </h1>
<p> 
    <a href="https://github.com/breezedeus/CnOCR">CnOCR 2.3.0.2</a>
    was used to test 64 images from the validation set of
    <a href="https://universe.roboflow.com/2014-series-license-plate/knn-brxiq"> Philippine 2014 License Plates.</a>
</p>
<h3> Results </h3>
<table>
    <tr>
        <th> Accuracy </th>
        <td> 0.760089686098 (76.0089686098%) </td>
    </tr>
</table>
<h3> Notes </h3>
<p> 
    Text from images were retrieved as a string. Some strings included non-alphanumeric characters along with the predicted license plate number. Testing was done by subtracting the total number of errors from the total number of characters, all over the total number of characters. Errors in this case, refer to substitutions (incorrect characters), insertions (extra characters), and deletions (missing characters). For example, if the ground truth license plate is "AAA1111" and the predicted license plate is "AAA111", then the total number of errors is 1 because the minimum number of operations (insert, delete or substitute) required to convert the ground truth license plate to the predicted license plate is 1 (delete a "1" from the ground truth license plate to make it equal to "AAA111").
</p>
<p>
    Each image is initially pre-processed by turning the RGB image to grayscale, applied with Gaussian blur of size 5 by 5, thresholded to a binary image, then dilated and eroded with a kernel size of 2 by 2.
</p>
<p>
    The formula used for finding the accuracy of the OCR engine is <code>(total - total_err) / total</code>, where <code>total</code> refers to the total number of characters of the ground truth license plates, and <code>total_err</code> refers to the total number of errors of the predicted license plates.
</p>
