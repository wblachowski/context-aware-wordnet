The plan is to grab all the synsets and all hypernyms for each of them, all the way up to the root.
After doing that for all the words from our list, we have some paths in the graph that occur more commonly, have more "weight".
This weight represents the support for this path in the whole set.

After this step, we go back to the original synstets. For every word, we consider its synstes and see which one has the greatest support.
This support has to be calculated somehow, let's say by calculating the average support for all its paths.
