const cache = new Map()

export const getWikipediaImage = async (animalName) => {
  if (!animalName) return null

  const cacheKey = animalName.toLowerCase()
  if (cache.has(cacheKey)) {
    return cache.get(cacheKey)
  }

  try {
    const searchResponse = await fetch(
      `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(animalName)}`
    )

    if (searchResponse.ok) {
      const data = await searchResponse.json()
      if (data.thumbnail && data.thumbnail.source) {
        const imageUrl = data.thumbnail.source.replace(/\/\d+px-/, '/300px-')
        cache.set(cacheKey, imageUrl)
        return imageUrl
      }
    }

    cache.set(cacheKey, null)
    return null
  } catch (error) {
    console.error('Failed to fetch Wikipedia image:', error)
    cache.set(cacheKey, null)
    return null
  }
}

export const preloadWikipediaImages = async (animalNames) => {
  const promises = animalNames.map(name => getWikipediaImage(name))
  await Promise.allSettled(promises)
}
