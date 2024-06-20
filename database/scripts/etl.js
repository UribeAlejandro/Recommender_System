var duplicates = [];

db.getSiblingDB("shein").getCollection("product_reviews").aggregate([
  { $match: {
    review: { "$ne": '' }  // discard selection criteria
  }},
  { $group: {
    _id: { review: "$review"}, // can be grouped on multiple properties
    dups: { "$addToSet": "$_id" },
    count: { "$sum": 1 }
  }},
  { $match: {
    count: { "$gt": 1 }    // Duplicates considered as count greater than one
  }}
],
{allowDiskUse: true}       // For faster processing if set is larger
)               // You can display result until this and check duplicates
.forEach(function(doc) {
    doc.dups.shift();      // First element skipped for deleting
    doc.dups.forEach( function(dupId){
        duplicates.push(dupId);   // Getting all duplicate ids
        }
    )
})

db.getSiblingDB("shein").getCollection("product_reviews").remove({_id:{$in:duplicates}})

db.getSiblingDB("shein").getCollection("product_reviews").aggregate([
  { $sortByCount: '$product_id' }
]);
