inline float4 mix(float4 a, float4 b, float t) {
  return (b - a) * clamp(t, 0.0f, 1.0f) + a;
}

kernel TexTile: ImageComputationKernel<ePixelWise> {

    Image<eRead, eAccessRandom, eEdgeClamped> src;
    Image<eWrite> dst;

    param:
        float width;
        float height;
        float tiling;
        float offset;
        float scale;
        float contrast;

    float4 hash4(float2 p) {
        float4 val =  sin(float4(1.0f + dot(p, float2(37.0f, 17.0f)), 
                                 2.0f + dot(p, float2(11.0f, 47.0f)),
                                 3.0f + dot(p, float2(41.0f, 29.0f)),
                                 4.0f + dot(p, float2(23.0f, 31.0f)))) * 103.0f;
        for (int i = 0; i < 4; i++)
            val[i] = fmod(val[i], 1.0f);
        return (val + 1) * 0.5f;
    }

    void process(int2 pos)
    {
        float2 uv = float2(
            (pos.x + 0.5f) / width,
            (pos.y + 0.5f) / height
        );

        uv *= tiling;

        float2 p = floor(uv);
        float2 f = float2(fmod(uv.x, 1.0f), fmod(uv.y, 1.0f));
        
        float4 va = 0;
        float w1 = 0;
        float w2 = 0;
        // Iterate over adjacent voronoi cells
        for (int j = -1; j <= 1; j++)
            for (int i = -1; i <= 1; i++)
            {
                // Create a voronoi cell point
                float2 g = float2(float(i), float(j));                 // Adjacent cell point
                float4 o = hash4(p + g);                               // Random offset
                float2 r = float2(g.x - f.x + o.x, g.y - f.y + o.y);   // Resulting co-ordinate

                float d = dot(r, r);                                   // length of offset
                float w = exp(-5.0f * d);                              // gaussian falloff
                
                // Use the offset to pick a pseudo-random point to sample
                // Using r instead of uv offsets from center of cell, allowing us to scale each individually
                float randf = (o.x - 0.5f) * scale + 1.0f;
                float x = r.x * randf + o.z * offset;
                float y = r.y * randf + o.w * offset;

                // Wrap x and y around image and sample
                x = fmod(fmod(x, 1.0f) + 1.0f, 1.0f) * width;
                y = fmod(fmod(y, 1.0f) + 1.0f, 1.0f) * height;
                float4 c = bilinear(src, x, y);
                
                // Accumulate weighted colour
                va += w * c;
                w1 += w;
                w2 += w * w;
            }
        
        // normal averaging --> lowers contrasts
        // float4 col = va / w1;

        float4 res = contrast + (va - w1 * contrast) / sqrt(w2);
        float4 col = mix(va / w1, res, offset);


        for (int c = 0; c < 3; c++)
            dst(c) = col[c];
        dst(3) = 1;

    }
};