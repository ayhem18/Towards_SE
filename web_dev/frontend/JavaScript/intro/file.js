const quote = 'I do not like green eggs and ham. I do not like them, Sam-I-Am.';
const substring = 'green eggs and ham';

quoteLength = quote.length;
index = quote.indexOf(substring);
console.log(`The subtring '${substring}' appears at the ${index + 1} -th index`);
revisitedQuote = quote.slice(0, index) + substring;
console.log(revisitedQuote);


/*
a bit about js arrays
*/

arrays = ["string1", "string2"]


