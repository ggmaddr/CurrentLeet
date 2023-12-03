
function recommendProducts(products, searchWord) {
    const recommendedProducts = [];
    for (let i = 0; i < searchWord.length; i++) {
        const currentPrefix = searchWord.substring(0, i + 1);
        const matchingProducts = [];
        // Filter products with the current prefix


        for (const product of products) {
            if (product.toLowerCase().startsWith(currentPrefix.toLowerCase())) {
                matchingProducts.push(product);
            }
        }

        // Sort matching products lexicographically
        matchingProducts.sort();
        // Limit the number of recommended products to 3 
        const recommendedProductsForCurrentPrefix = matchingProducts.slice(0, 3);
        recommendedProducts.push(recommendedProductsForCurrentPrefix);
    }

    return recommendedProducts;

}
products = ["mobile", "mouse", "moneypot", "monitor", "mousepad"]
searchWord = "mouse"
