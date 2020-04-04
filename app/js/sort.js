/**
 * Generic sorting functon
 * @param {array} data - The array of data to be sorted
 * @param {string} sortParam - The parameter to sort the data by
 * @param {string} sortOrder - The order to sort by A -> Z or Z -> A
 * @returns {array} - The sorted data
 */

export default function sort(data, sortParam, sortOrder) {
  function checkIfLetters(value) {
    const regex = RegExp("^d");
    return regex.test(value);
  }
  let sortedData;

  if (sortOrder === "az") {
    sortedData = data.sort(function(a, b) {
      let aParam = a[sortParam];
      let bParam = b[sortParam];

      const aIsLetters = checkIfLetters(aParam);
      const bIsLetters = checkIfLetters(bParam);
      if (typeof aParam === "string" && aIsLetters && bIsLetters) {
        aParam = aParam.toUpperCase(); // ignore upper and lowercase
        bParam = bParam.toUpperCase(); // ignore upper and lowercase
      }

      if (aParam < bParam) {
        return -1;
      }
      if (aParam > bParam) {
        return 1;
      }
      // names must be equal
      return 0;
    });
  } else if (sortOrder === "za") {
    sortedData = data.sort(function(a, b) {
      let aParam = a[sortParam];
      let bParam = b[sortParam];

      const aIsLetters = checkIfLetters(aParam);
      const bIsLetters = checkIfLetters(bParam);
      if (typeof aParam === "string" && aIsLetters && bIsLetters) {
        aParam = aParam.toUpperCase(); // ignore upper and lowercase
        bParam = bParam.toUpperCase(); // ignore upper and lowercase
      }

      if (aParam < bParam) {
        return 1;
      }
      if (aParam > bParam) {
        return -1;
      }
      // names must be equal
      return 0;
    });
  }
  return sortedData;
}
